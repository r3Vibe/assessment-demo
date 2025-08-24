interface IMessagesProps {
  messages: Array<{
    type: "human" | "ai";
    image?: string;
    displayText: string;
  }>;
}

import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";

export default function Messages({ messages }: IMessagesProps) {
  return (
    <>
      {messages.map((message, index) => (
        <div
          key={index}
          style={{
            padding: "10px",
            width: "500px",
            backgroundColor:
              message.type === "human"
                ? "var(--primary-color)"
                : "var(--surface-card)",
            color: message.type === "human" ? "white" : "var(--text-color)",
            borderRadius: "8px",
            maxWidth: "80%",
            alignSelf: message.type === "human" ? "flex-end" : "flex-start",
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          }}
        >
          {message.image ? (
            <img
              src={`data:image/png;base64,${message.image}`}
              alt="Message attachment"
              style={{
                maxWidth: "100%",
                borderRadius: "4px",
                objectFit: "contain",
                height: "auto",
              }}
            />
          ) : (
            <div style={{ whiteSpace: "pre-wrap" }}>
              <ReactMarkdown
                rehypePlugins={[rehypeSanitize]}
                remarkPlugins={[remarkGfm]}
              >
                {message.displayText}
              </ReactMarkdown>
            </div>
          )}
        </div>
      ))}
    </>
  );
}
