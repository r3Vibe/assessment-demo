import { ScrollPanel } from "primereact/scrollpanel";

export default function MessageBox({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ScrollPanel
      style={{
        width: "100%",
        height: "auto",
        minHeight: "650px",
        border: "1px solid var(--surface-border)",
        borderRadius: "15px",
        padding: "10px",
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {children}
      </div>
    </ScrollPanel>
  );
}
