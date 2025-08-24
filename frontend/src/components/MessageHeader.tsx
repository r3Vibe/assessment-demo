import { Button } from "primereact/button";
import type { Message } from "../Types";

export default function MessageHeader({
  chatid,
  setChatid,
  setMessages,
}: {
  chatid: string;
  setChatid: React.Dispatch<React.SetStateAction<string>>;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}) {
  return (
    <div
      style={{
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "15px",
        borderBottom: "1px solid #eee",
      }}
    >
      <h4 style={{ margin: 0 }}>Chat ID: {chatid}</h4>
      <Button
        label="New Chat"
        icon="pi pi-plus"
        onClick={() => {
          const newChatId = Date.now().toString();
          setChatid(newChatId);
          setMessages([]);
          localStorage.setItem("chatid", newChatId);
        }}
      />
    </div>
  );
}
