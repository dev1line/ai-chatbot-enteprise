import type { Citation } from "../api/client";

export function Citations({ citations }: { citations: Citation[] }) {
  if (!citations || citations.length === 0) return null;
  return (
    <div className="citations">
      <div className="citations-title">Citations ({citations.length})</div>
      <ul>
        {citations.map((c, i) => (
          <li key={i}>
            <span className={`tag tag-${c.type}`}>{c.type}</span>{" "}
            <strong>{c.doc_id}</strong>
            {c.version ? ` · ${c.version}` : ""}
            {c.page != null ? ` · page ${c.page}` : ""}
            {c.sheet ? ` · sheet ${c.sheet}` : ""}
            {c.cell_range ? ` · ${c.cell_range}` : ""}
            {c.snippet ? <div className="snippet">{c.snippet}</div> : null}
          </li>
        ))}
      </ul>
    </div>
  );
}
