function renderInline(text) {
  if (!text) return null;

  const tokens = [];
  let i = 0;

  const pushText = (t) => {
    if (t) tokens.push(t);
  };

  while (i < text.length) {
    const rest = text.slice(i);

    // Bold **...**
    if (rest.startsWith("**")) {
      const end = rest.indexOf("**", 2);
      if (end !== -1) {
        const content = rest.slice(2, end);
        tokens.push(<strong key={`b-${i}`}>{renderInline(content)}</strong>);
        i += end + 2;
        continue;
      }
    }

    // Italic *...* (skip **)
    if (rest.startsWith("*") && !rest.startsWith("**")) {
      const end = rest.indexOf("*", 1);
      if (end !== -1) {
        const content = rest.slice(1, end);
        tokens.push(<em key={`i-${i}`}>{renderInline(content)}</em>);
        i += end + 1;
        continue;
      }
    }

    // Inline code `...`
    if (rest.startsWith("`")) {
      const end = rest.indexOf("`", 1);
      if (end !== -1) {
        const content = rest.slice(1, end);
        tokens.push(
          <code
            key={`c-${i}`}
            style={{
              fontFamily:
                "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
              fontSize: "0.95em",
              padding: "2px 6px",
              borderRadius: 10,
              background: "rgba(15, 23, 42, 0.06)",
              border: "1px solid rgba(15, 23, 42, 0.08)",
            }}
          >
            {content}
          </code>
        );
        i += end + 1;
        continue;
      }
    }

    // Plain text: consume until next marker
    const nextMarkers = ["**", "*", "`"]
      .map((m) => rest.indexOf(m, 1))
      .filter((idx) => idx !== -1);
    const next = nextMarkers.length ? Math.min(...nextMarkers) : -1;
    if (next === -1) {
      pushText(rest);
      break;
    }
    pushText(rest.slice(0, next));
    i += next;
  }

  return tokens;
}

export default function Markdown({ text, className }) {
  const lines = (text || "").split(/\r?\n/);

  const blocks = [];
  let list = null;

  const flushList = () => {
    if (list?.length) {
      blocks.push(
        <ul key={`ul-${blocks.length}`} style={{ margin: 0, paddingLeft: 18 }}>
          {list.map((item, idx) => (
            <li key={idx} style={{ margin: "6px 0" }}>
              {renderInline(item)}
            </li>
          ))}
        </ul>
      );
    }
    list = null;
  };

  for (let idx = 0; idx < lines.length; idx += 1) {
    const raw = lines[idx];
    const line = raw.trimEnd();
    const t = line.trim();

    if (!t) {
      flushList();
      continue;
    }

    // Headings ### / ## / #
    const m = t.match(/^(#{1,6})\s+(.*)$/);
    if (m) {
      flushList();
      const level = m[1].length;
      const content = m[2];
      const Tag = level <= 3 ? "h3" : "h4";
      blocks.push(
        <Tag
          key={`h-${idx}`}
          style={{
            margin: idx === 0 ? 0 : "12px 0 6px",
            fontSize: Tag === "h3" ? 14 : 13,
            letterSpacing: "-0.01em",
          }}
        >
          {renderInline(content)}
        </Tag>
      );
      continue;
    }

    // Bullet list: * item or - item
    const b = t.match(/^[-*]\s+(.*)$/);
    if (b) {
      if (!list) list = [];
      list.push(b[1]);
      continue;
    }

    flushList();
    blocks.push(
      <p key={`p-${idx}`} style={{ margin: blocks.length ? "10px 0 0" : 0 }}>
        {renderInline(t)}
      </p>
    );
  }
  flushList();

  return (
    <div className={className} style={{ whiteSpace: "normal" }}>
      {blocks.length ? blocks : <span>{text}</span>}
    </div>
  );
}

