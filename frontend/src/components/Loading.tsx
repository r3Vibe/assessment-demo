export default function Loading() {
  return (
    <div
      style={{
        padding: "10px",
        backgroundColor: "var(--surface-card)",
        borderRadius: "8px",
        maxWidth: "80%",
        alignSelf: "flex-start",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        color: "var(--text-color)",
      }}
    >
      <div style={{ display: "flex", gap: "3px", alignItems: "center" }}>
        <span
          style={{
            animation: "typingDot 1s infinite",
            animationDelay: "0s",
            fontSize: "20px",
          }}
        >
          ●
        </span>
        <span
          style={{
            animation: "typingDot 1s infinite",
            animationDelay: "0.2s",
            fontSize: "20px",
          }}
        >
          ●
        </span>
        <span
          style={{
            animation: "typingDot 1s infinite",
            animationDelay: "0.4s",
            fontSize: "20px",
          }}
        >
          ●
        </span>
      </div>
    </div>
  );
}
