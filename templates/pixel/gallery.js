(function () {
    'use strict';

    // ---- build grids ----

    document.querySelectorAll('.gallery').forEach(function (galleryEl) {
        var ul = galleryEl.querySelector('ul');
        if (!ul) return;

        var items = [];
        var grid  = document.createElement('div');
        grid.className = 'gallery-grid';

        Array.from(ul.children).forEach(function (li) {
            if (li.tagName !== 'LI') return;

            var img = li.querySelector('img');
            if (!img) return;

            var desc  = [];
            var tools = null;
            var colors = null;

            li.querySelectorAll(':scope > ul > li').forEach(function (sub) {
                var text = sub.textContent.trim();
                if (text.startsWith('Colors:')) {
                    var parts = text.replace('Colors:', '').trim().split(/\s+/);
                    colors = { fg: parts[0] || null, bg: parts[1] || null };
                } else if (text.startsWith('Tools:')) {
                    tools = text.replace('Tools:', '').trim().split(/\s*,\s*/);
                } else if (text) {
                    desc.push(text);
                }
            });

            items.push({
                src:    img.getAttribute('src'),
                alt:    img.alt || '',
                desc:   desc,
                tools:  tools,
                colors: colors,
            });

            var cell  = document.createElement('div');
            cell.className = 'gallery-item';
            var thumb = document.createElement('img');
            thumb.src     = img.getAttribute('src');
            thumb.alt     = img.alt || '';
            thumb.loading = 'lazy';
            cell.appendChild(thumb);
            cell.addEventListener('click', (function (idx) {
                return function () { openLightbox(items, idx); };
            }(items.length - 1)));
            grid.appendChild(cell);
        });

        ul.replaceWith(grid);
    });

    // ---- lightbox ----

    var lb = document.createElement('div');
    lb.id = 'lb';
    lb.innerHTML =
        '<div id="lb-bg"></div>' +
        '<button id="lb-prev" aria-label="Previous">&#8592;</button>' +
        '<div id="lb-panel">' +
            '<img id="lb-img" alt="" />' +
            '<p id="lb-caption"></p>' +
            '<p id="lb-desc"></p>' +
            '<ul id="lb-tools"></ul>' +
        '</div>' +
        '<button id="lb-next" aria-label="Next">&#8594;</button>' +
        '<button id="lb-close" aria-label="Close">&#x2715;</button>';
    document.body.appendChild(lb);

    var lbPanel = document.getElementById('lb-panel');
    var lbImg   = document.getElementById('lb-img');
    var lbCap   = document.getElementById('lb-caption');
    var lbDesc  = document.getElementById('lb-desc');
    var lbTools = document.getElementById('lb-tools');

    var currentItems = null;
    var currentIdx   = 0;

    function show() {
        var item = currentItems[currentIdx];

        lbImg.src = item.src;
        lbImg.alt = item.alt;

        lbCap.textContent  = item.alt;
        lbCap.style.display = item.alt ? '' : 'none';

        lbDesc.textContent  = item.desc.join(' ');
        lbDesc.style.display = item.desc.length ? '' : 'none';

        lbTools.innerHTML = '';
        if (item.tools && item.tools.length) {
            item.tools.forEach(function (t) {
                var li = document.createElement('li');
                li.textContent = t.trim();
                lbTools.appendChild(li);
            });
            lbTools.style.display = '';
        } else {
            lbTools.style.display = 'none';
        }

        if (item.colors) {
            lbPanel.style.color           = item.colors.fg || '';
            lbPanel.style.backgroundColor = item.colors.bg || '';
        } else {
            lbPanel.style.color           = '';
            lbPanel.style.backgroundColor = '';
        }
    }

    function openLightbox(items, idx) {
        currentItems = items;
        currentIdx   = idx;
        show();
        lb.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lb.classList.remove('open');
        document.body.style.overflow = '';
        currentItems = null;
    }

    function prev() { currentIdx = (currentIdx - 1 + currentItems.length) % currentItems.length; show(); }
    function next() { currentIdx = (currentIdx + 1) % currentItems.length; show(); }

    // ---- index list ----

    document.querySelectorAll('.index-list li').forEach(function (li) {
        var textNode = Array.from(li.childNodes).find(function (n) {
            return n.nodeType === Node.TEXT_NODE && n.textContent.trim();
        });
        if (!textNode) return;
        var desc = textNode.textContent.replace(/^\s*-\s*/, '').trim();
        textNode.remove();
        if (desc) {
            var p = document.createElement('p');
            p.className = 'index-desc';
            p.textContent = desc;
            li.appendChild(p);
        }
    });

    document.getElementById('lb-bg').addEventListener('click', closeLightbox);
    document.getElementById('lb-close').addEventListener('click', closeLightbox);
    document.getElementById('lb-prev').addEventListener('click', prev);
    document.getElementById('lb-next').addEventListener('click', next);

    document.addEventListener('keydown', function (e) {
        if (!currentItems) return;
        if (e.key === 'ArrowLeft')  prev();
        if (e.key === 'ArrowRight') next();
        if (e.key === 'Escape')     closeLightbox();
    });
}());
