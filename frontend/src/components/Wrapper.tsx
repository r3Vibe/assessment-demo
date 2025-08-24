export default function Wrapper({ children }: { children: React.ReactNode }) {
  return (
    <div
      style={{
        padding: "25px",
        width: "100%",
        height: "90vh",
        display: "flex",
        flexDirection: "column",
        gap: "20px",
      }}
    >
      {children}
    </div>
  );
}
