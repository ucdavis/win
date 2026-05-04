-- div-anchors.lua
-- Adds visual URL anchor links to theorem and proof divs for HTML and
-- RevealJS output, matching the chain-link icon style of Quarto heading
-- anchors and following the same inline-script approach as equation-anchors.
--
-- This approach uses a Pandoc filter to inject a raw HTML script block
-- because Quarto processes theorem divs as custom AST nodes that are not
-- visible to Lua element filters at extension filter time.

local function in_html_output()
  if quarto and quarto.doc and quarto.doc.is_format then
    return quarto.doc.is_format("html") or quarto.doc.is_format("revealjs")
  end

  return false
end

local function anchor_script()
  return [[
<script>
(function () {
  "use strict";

  /**
   * CSS selector matching all Quarto theorem and proof div environments.
   *
   * Quarto adds the `.theorem` class to all theorem-type divs
   * (theorem, lemma, corollary, proposition, conjecture, definition,
   * example, exercise, algorithm), so `.theorem[id]` covers all of them.
   * Proof-type environments (.proof, .remark, .solution) are listed
   * separately because they do not carry the `.theorem` class.
   */
  var THEOREM_SELECTOR = [
    ".theorem[id]",
    ".proof[id]",
    ".remark[id]",
    ".solution[id]",
  ].join(", ");

  function getQuartoHeadingAnchorIcon() {
    var afterBodyScript = document.getElementById("quarto-html-after-body");
    if (!afterBodyScript) {
      return null;
    }

    var match = afterBodyScript.textContent.match(/const icon = ["']([^"']+)["']/);
    return match ? match[1] : null;
  }

  // Quarto chain-link glyph from Bootstrap Icons.
  var chainLinkIconFallback = "\ue9cb";
  var headingAnchorIcon = getQuartoHeadingAnchorIcon();
  var defaultAnchorIconFallback =
    headingAnchorIcon && headingAnchorIcon !== "#" ? headingAnchorIcon : chainLinkIconFallback;

  function getDefaultAnchorTemplate() {
    var defaultAnchor =
      document.querySelector(".anchored > a.anchorjs-link") ||
      document.querySelector("a.anchorjs-link[data-anchorjs-icon]");
    if (!defaultAnchor) {
      return null;
    }

    return {
      icon: defaultAnchor.getAttribute("data-anchorjs-icon") || defaultAnchor.textContent.trim(),
      hasDataIcon: defaultAnchor.hasAttribute("data-anchorjs-icon"),
      style: defaultAnchor.getAttribute("style")
    };
  }

  function normalizeAnchorIcon(icon) {
    if (!icon || icon === "#") {
      return defaultAnchorIconFallback;
    }

    return icon;
  }

  function createChainLinkSvgIcon() {
    var svgNs = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(svgNs, "svg");
    svg.setAttribute("viewBox", "0 0 16 16");
    svg.setAttribute("fill", "currentColor");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    svg.setAttribute("class", "div-anchor-icon");

    // Bootstrap Icons chain-link icon (bi-link-45deg), paths for the two
    // chain links and the connecting segment.
    [
      "M6.354 5.5H4a3 3 0 0 0 0 6h3a3 3 0 0 0 2.83-2H11a4 4 0 0 1-4 3H4a4 4 0 0 1 0-8h2.354z",
      "M9.646 10.5H12a3 3 0 1 0 0-6H9a3 3 0 0 0-2.83 2H5a4 4 0 0 1 4-3h3a4 4 0 0 1 0 8H9.646z",
      "M5.5 8a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1-.5-.5"
    ].forEach(function (pathData) {
      var path = document.createElementNS(svgNs, "path");
      path.setAttribute("d", pathData);
      svg.appendChild(path);
    });

    return svg;
  }

  function alignDivAnchorWithDefault(anchor, template) {
    if (!anchor) {
      return;
    }

    anchor.classList.remove("external");
    anchor.classList.add("no-external");

    var normalizedIcon = normalizeAnchorIcon(template && template.icon);
    if (normalizedIcon === chainLinkIconFallback) {
      anchor.removeAttribute("data-anchorjs-icon");
      anchor.textContent = "";
      anchor.appendChild(createChainLinkSvgIcon());
    } else if (template && template.hasDataIcon) {
      anchor.setAttribute("data-anchorjs-icon", normalizedIcon);
      anchor.textContent = normalizedIcon;
    } else {
      anchor.removeAttribute("data-anchorjs-icon");
      anchor.textContent = normalizedIcon;
    }

    if (template && template.style) {
      anchor.setAttribute("style", template.style);
    } else {
      anchor.removeAttribute("style");
    }
  }

  function alignDivAnchorsWithDefault() {
    var template = getDefaultAnchorTemplate();
    document.querySelectorAll("a.div-anchor").forEach(function (anchor) {
      alignDivAnchorWithDefault(anchor, template);
    });
  }

  function ensureDivAnchorStyles() {
    if (document.getElementById("div-anchor-styles")) {
      return;
    }

    var style = document.createElement("style");
    style.id = "div-anchor-styles";
    style.textContent = [
      ".div-anchor {",
      "  opacity: 0;",
      "  font-size: 0.875em;",
      "  font-weight: 400;",
      "  margin-left: 0.375em;",
      "  text-decoration: none;",
      "  color: inherit;",
      "  vertical-align: middle;",
      "  transition: opacity 0.2s ease;",
      "}",
      ".div-anchor:hover,",
      ".div-anchor:focus {",
      "  opacity: 1;",
      "  text-decoration: none;",
      "}",
      ".div-anchor-icon {",
      "  width: 0.875em;",
      "  height: 0.875em;",
      "  vertical-align: -0.125em;",
      "}",
      ":is(.theorem, .proof, .remark, .solution):hover .div-anchor,",
      ":is(.theorem, .proof, .remark, .solution):focus-within .div-anchor {",
      "  opacity: 1;",
      "}"
    ].join("\n");
    document.head.appendChild(style);
  }

  /**
   * Add anchor links to all theorem/proof divs with ids on the page.
   */
  function addDivAnchors() {
    ensureDivAnchorStyles();

    var divs = document.querySelectorAll(THEOREM_SELECTOR);
    divs.forEach(function (div) {
      var id = div.id;
      if (!id) {
        return;
      }

      // Skip if already processed.
      if (div.querySelector(".div-anchor")) {
        return;
      }

      var anchor = document.createElement("a");
      anchor.className = "div-anchor anchorjs-link";
      anchor.href = "#" + id;
      anchor.setAttribute("aria-label", "Permalink to this block");
      anchor.classList.add("no-external");

      // Find the theorem-title or proof-title span
      var titleSpan = div.querySelector(".theorem-title, .proof-title");

      if (titleSpan) {
        // Insert anchor immediately after the title span
        titleSpan.insertAdjacentElement("afterend", anchor);
      } else {
        // Fallback: prepend to the first paragraph
        var firstPara = div.querySelector("p");
        if (firstPara) {
          firstPara.insertAdjacentElement("afterbegin", anchor);
        }
      }
    });

    alignDivAnchorsWithDefault();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addDivAnchors);
  } else {
    addDivAnchors();
  }

  window.addEventListener("load", alignDivAnchorsWithDefault);
})();
</script>
]]
end

function Pandoc(doc)
  if not in_html_output() then
    return nil
  end

  table.insert(doc.blocks, pandoc.RawBlock("html", anchor_script()))
  return doc
end
