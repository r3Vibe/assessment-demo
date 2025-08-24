import { Button } from "primereact/button";
import { InputTextarea } from "primereact/inputtextarea";
import { useState } from "react";
import type { Socket } from "socket.io-client";
import type { Message } from "../Types";

export default function MessagePanel({
  isConnected,
  socketRef,
  fileupload,
  setMessages,
  setVisible,
  setFileupload,
  chatid,
}: {
  isConnected: boolean;
  socketRef: React.RefObject<Socket | null>;
  fileupload: string | null;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  setVisible: React.Dispatch<React.SetStateAction<boolean>>;
  setFileupload: React.Dispatch<React.SetStateAction<string | null>>;
  chatid: string;
}) {
  const [value, setValue] = useState<string>("");
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        gap: "10px",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <InputTextarea
        variant="filled"
        value={value}
        onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
          setValue(e.target.value)
        }
        rows={5}
        cols={30}
        style={{ flexGrow: 1 }}
        placeholder="Type a message..."
      />
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          gap: "10px",
          flexDirection: "column",
        }}
      >
        <Button icon="pi pi-upload" onClick={() => setVisible(true)} />
        <Button
          icon="pi pi-send"
          disabled={!isConnected}
          severity={isConnected ? "success" : "secondary"}
          onClick={() => {
            if (socketRef.current && value.trim()) {
              // Add human message immediately
              const humanMessage: Message = {
                text: value,
                displayText: value,
                isTyping: false,
                type: "human",
              };
              setMessages((prev) => [...prev, humanMessage]);

              // Send to server
              socketRef.current.emit("message", {
                message: value,
                message_type: !fileupload ? "text" : "file",
                file: fileupload,
                chat_id: chatid,
              });
              setValue("");

              setFileupload(null);
            }
          }}
        />
      </div>
    </div>
  );
}
