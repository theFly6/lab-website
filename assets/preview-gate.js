// 仅用于演示访问码遮罩；正文与校验摘要均公开，可通过开发工具绕过。
(() => {
  'use strict';
  const gate = document.querySelector('#preview-gate');
  if (!gate) return;

  const root = document.documentElement;
  const form = gate.querySelector('form');
  const input = gate.querySelector('input');
  const submit = gate.querySelector('button[type="submit"]');
  const status = gate.querySelector('[role="status"]');
  const expected = gate.dataset.codeSha256;
  // 同一github.io域名下的不同仓库分别记忆；修改摘要后旧会话自动失效。
  const storageKey = `lab-preview:${gate.dataset.storageScope}`;

  const unlock = (restoreFocus = false) => {
    input.value = '';
    root.removeAttribute('data-preview-gate');
    if (gate.open && typeof gate.close === 'function') gate.close();
    else gate.removeAttribute('open');
    if (restoreFocus) document.querySelector('main')?.focus({ preventScroll: true });
  };

  try {
    if (sessionStorage.getItem(storageKey) === expected && /^[a-f0-9]{64}$/.test(expected)) {
      unlock();
      return;
    }
  } catch {
    // 隐私模式禁用存储时仍允许验证当前页面，不依赖跨页面记忆。
  }

  // 原生模态对话框负责背景惰性与焦点限制，Escape不能跳过验证。
  gate.addEventListener('cancel', event => event.preventDefault());
  gate.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
    }
  });
  if (typeof gate.showModal !== 'function') {
    gate.setAttribute('open', '');
    status.textContent = gate.dataset.unavailable;
    return;
  }
  gate.close();
  gate.showModal();
  status.textContent = '';
  input.focus({ preventScroll: true });
  if (!/^[a-f0-9]{64}$/.test(expected)) {
    status.textContent = gate.dataset.configError;
    return;
  }
  if (!window.crypto?.subtle || typeof TextEncoder === 'undefined') {
    status.textContent = gate.dataset.unavailable;
    return;
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (submit.disabled) return;
    if (!input.value.trim()) {
      input.setAttribute('aria-invalid', 'true');
      status.textContent = gate.dataset.invalid;
      input.focus();
      return;
    }
    submit.disabled = true;
    status.textContent = '';
    try {
      const bytes = new TextEncoder().encode(input.value.trim());
      const digest = await crypto.subtle.digest('SHA-256', bytes);
      const actual = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
      if (actual !== expected) {
        input.setAttribute('aria-invalid', 'true');
        status.textContent = gate.dataset.invalid;
        input.focus();
        input.select();
        return;
      }
      try {
        sessionStorage.setItem(storageKey, expected);
      } catch {
        // 无法记忆时只放行当前页面，下次访问仍可重新输入。
      }
      input.removeAttribute('aria-invalid');
      status.textContent = '';
      unlock(true);
    } catch {
      status.textContent = gate.dataset.unavailable;
    } finally {
      submit.disabled = false;
    }
  });
  input.addEventListener('input', () => {
    input.removeAttribute('aria-invalid');
    status.textContent = '';
  });
  submit.disabled = false;
})();
