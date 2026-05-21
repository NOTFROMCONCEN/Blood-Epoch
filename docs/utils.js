/* ===== utils.js — Shared utilities for 2019血疫纪元 website ===== */

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/**
 * Inline markdown formatting: bold, italic, code, links, line breaks
 */
function inlineFormat(text) {
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
  text = text.replace(/\n/g, '<br>');
  return text;
}

/**
 * Show a toast notification (auto-dismiss after 2s)
 */
function showToast(message) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2000);
}

/**
 * Throttle function using requestAnimationFrame
 */
function rafThrottle(fn) {
  let ticking = false;
  return function(...args) {
    if (!ticking) {
      requestAnimationFrame(() => {
        fn.apply(this, args);
        ticking = false;
      });
      ticking = true;
    }
  };
}

/**
 * Full markdown → HTML renderer (for article content)
 * Supports: headings, bold, italic, code, blockquotes, lists, tables, hr, meta blocks
 */
function renderMarkdown(md) {
  if (!md) return '';

  md = md.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  let html = '';
  const lines = md.split('\n');
  let inCodeBlock = false;
  let inTable = false;
  let tableRows = [];
  let inList = false;
  let listType = '';
  let listItems = [];
  let paragraph = [];

  function flushParagraph() {
    if (paragraph.length > 0) {
      const text = paragraph.join('\n');
      if (isMetaBlock(text)) {
        html += '<div class="meta-block">' + inlineFormat(escapeHtml(text)) + '</div>';
      } else {
        html += '<p>' + inlineFormat(escapeHtml(text)) + '</p>';
      }
      paragraph = [];
    }
  }

  function flushList() {
    if (listItems.length > 0) {
      const tag = listType === 'ol' ? 'ol' : 'ul';
      html += '<' + tag + '>' + listItems.map(function(i) { return '<li>' + inlineFormat(escapeHtml(i)) + '</li>'; }).join('') + '</' + tag + '>';
      listItems = [];
      inList = false;
    }
  }

  function flushTable() {
    if (tableRows.length > 0) {
      html += '<table>';
      tableRows.forEach(function(row, i) {
        var tag = i === 0 ? 'th' : 'td';
        if (i === 0) html += '<thead><tr>';
        else if (i === 1) { /* separator, skip */ }
        else { if (i === 2) html += '<tbody>'; html += '<tr>'; }

        if (i !== 1) {
          row.forEach(function(cell) {
            html += '<' + tag + '>' + inlineFormat(escapeHtml(cell.trim())) + '</' + tag + '>';
          });
        }

        if (i === 0) html += '</tr></thead>';
        else if (i === 1) { /* skip */ }
        else html += '</tr>';
      });
      html += '</tbody></table>';
      tableRows = [];
      inTable = false;
    }
  }

  function isMetaBlock(text) {
    var lines = text.split('\n');
    var boldCount = 0;
    lines.forEach(function(l) { if (l.match(/^\*\*[^*]+:\s*/)) boldCount++; });
    return boldCount >= 2 && boldCount >= lines.length * 0.5;
  }

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    var trimmed = line.trim();

    // Code block
    if (trimmed.startsWith('```')) {
      if (inCodeBlock) {
        html += '</pre>';
        inCodeBlock = false;
      } else {
        flushParagraph(); flushList(); flushTable();
        html += '<pre>';
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      html += escapeHtml(line) + '\n';
      continue;
    }

    // Horizontal rule / scene break
    if (/^---+\s*$/.test(trimmed) || /^\*\*\*+\s*$/.test(trimmed)) {
      flushParagraph(); flushList(); flushTable();
      html += '<div class="scene-break">&middot; &middot; &middot;</div>';
      continue;
    }

    // Empty line
    if (!trimmed) {
      flushParagraph(); flushList(); flushTable();
      continue;
    }

    // Headers
    var hMatch = trimmed.match(/^(#{1,4})\s+(.+)/);
    if (hMatch) {
      flushParagraph(); flushList(); flushTable();
      var level = hMatch[1].length;
      html += '<h' + level + '>' + inlineFormat(escapeHtml(hMatch[2])) + '</h' + level + '>';
      continue;
    }

    // Table row
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushParagraph(); flushList();
      if (!inTable) inTable = true;
      var cells = trimmed.split('|').filter(function(c) { return c.trim() !== ''; });
      tableRows.push(cells);
      continue;
    }

    // Unordered list
    if (/^[-*+]\s+/.test(trimmed)) {
      flushParagraph(); flushTable();
      if (!inList) { inList = true; listType = 'ul'; }
      listItems.push(trimmed.replace(/^[-*+]\s+/, ''));
      continue;
    }

    // Ordered list
    if (/^\d+\.\s+/.test(trimmed)) {
      flushParagraph(); flushTable();
      if (!inList) { inList = true; listType = 'ol'; }
      listItems.push(trimmed.replace(/^\d+\.\s+/, ''));
      continue;
    }

    // Blockquote
    if (trimmed.startsWith('>')) {
      flushParagraph(); flushList(); flushTable();
      var quoteLines = [];
      while (i < lines.length && lines[i].trim().startsWith('>')) {
        quoteLines.push(lines[i].trim().replace(/^>\s?/, ''));
        i++;
      }
      i--;
      html += '<blockquote>' + inlineFormat(escapeHtml(quoteLines.join('\n'))) + '</blockquote>';
      continue;
    }

    if (inList) flushList();
    if (inTable) flushTable();

    // Regular paragraph
    paragraph.push(trimmed);
  }

  flushParagraph(); flushList(); flushTable();

  return html;
}
