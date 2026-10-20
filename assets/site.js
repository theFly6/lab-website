// 移动导航与论文筛选采用渐进增强，关闭 JavaScript 后仍可阅读全部正文。
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
const dropdowns = [...document.querySelectorAll('.nav-dropdown')];
const closeDropdowns = () => dropdowns.forEach(dropdown => { dropdown.open = false; });
// 原生 details 支持点击、触摸与键盘，无脚本时也可展开子导航。
dropdowns.forEach(dropdown => {
  dropdown.addEventListener('focusout', event => {
    if (event.relatedTarget && !dropdown.contains(event.relatedTarget)) dropdown.open = false;
  });
});
document.addEventListener('click', event => {
  if (!event.target.closest('.nav-dropdown')) closeDropdowns();
});
if (menu && navigation) {
  document.documentElement.classList.add('js');
  const closeMenu = () => {
    closeDropdowns();
    menu.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  };
  menu.addEventListener('click', () => {
    const expanded = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(expanded));
    navigation.classList.toggle('is-open', expanded);
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (document.querySelector('.floating-contact[open]')) return;
    const openDropdown = dropdowns.find(dropdown => dropdown.open);
    if (openDropdown) {
      openDropdown.open = false;
      openDropdown.querySelector('summary').focus();
    } else if (menu.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menu.focus();
    }
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
}
// 联系卡片保持为非模态区域；失败时显示真实的手动复制提示。
const floatingContact = document.querySelector('.floating-contact');
if (floatingContact) {
  const trigger = floatingContact.querySelector('summary');
  const closeButton = floatingContact.querySelector('.floating-contact-close');
  const copyButton = floatingContact.querySelector('.floating-contact-copy');
  const status = floatingContact.querySelector('.floating-contact-status');
  const closeContact = (restoreFocus = false) => {
    floatingContact.open = false;
    status.textContent = '';
    if (restoreFocus) trigger.focus();
  };
  closeButton.hidden = false;
  copyButton.hidden = false;
  closeButton.addEventListener('click', () => closeContact(true));
  floatingContact.addEventListener('toggle', () => {
    if (!floatingContact.open) status.textContent = '';
  });
  document.addEventListener('click', event => {
    if (!floatingContact.contains(event.target)) closeContact();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && floatingContact.open) {
      event.preventDefault();
      closeContact(true);
    }
  });
  floatingContact.addEventListener('focusout', event => {
    if (event.relatedTarget && !floatingContact.contains(event.relatedTarget)) closeContact();
  });
  copyButton.addEventListener('click', async () => {
    copyButton.disabled = true;
    status.textContent = '';
    try {
      await navigator.clipboard.writeText(floatingContact.dataset.email);
      if (floatingContact.open) status.textContent = floatingContact.dataset.copied;
    } catch {
      if (floatingContact.open) {
        const range = document.createRange();
        range.selectNodeContents(floatingContact.querySelector('.floating-contact-email'));
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = floatingContact.dataset.copyFailed;
      }
    } finally {
      copyButton.disabled = false;
    }
  });
}
const search = document.querySelector('#publication-search');
if (search) {
  const year = document.querySelector('#publication-year');
  const topic = document.querySelector('#publication-topic');
  const papers = [...document.querySelectorAll('[data-publication]')];
  const count = document.querySelector('#publication-count');
  const filter = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const paper of papers) {
      const matched = (!year.value || paper.dataset.year === year.value)
        && (!topic.value || paper.dataset.topic === topic.value)
        && paper.textContent.toLocaleLowerCase().includes(query);
      paper.hidden = !matched;
      if (matched) visible++;
    }
    count.textContent = count.dataset.template.replace('{count}', String(visible));
    document.querySelector('#publication-empty').hidden = visible !== 0;
  };
  [search, year, topic].forEach(control => {
    control.addEventListener('input', filter);
    control.addEventListener('change', filter);
  });
  filter();
}
