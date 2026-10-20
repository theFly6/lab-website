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
