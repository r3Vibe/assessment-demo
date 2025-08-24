import { Toast } from "primereact/toast";
import { useEffect, useRef, useState } from "react";
import { io, Socket } from "socket.io-client";
import Fileuploader from "./components/Fileuploader";
import Loading from "./components/Loading";
import MessageBox from "./components/MessageBox";
import MessageHeader from "./components/MessageHeader";
import MessagePanel from "./components/MessagePanel";
import Messages from "./components/Messages";
import Wrapper from "./components/Wrapper";
import type { Message } from "./Types";

// Add keyframe animation styles
const typingAnimation = `
  @keyframes typingDot {
    0% { opacity: 0.2; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1); }
    100% { opacity: 0.2; transform: scale(0.8); }
  }
`;

export default function App() {
  const [fileupload, setFileupload] = useState<string | null>(null);
  const [visible, setVisible] = useState(false);
  const [chatid, setChatid] = useState<string>("");
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const socketRef = useRef<Socket | null>(null);
  const toast = useRef<Toast>(null);

  // Inject animation styles
  useEffect(() => {
    const style = document.createElement("style");
    style.textContent = typingAnimation;
    document.head.appendChild(style);
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  useEffect(() => {
    const localChatId = localStorage.getItem("chatid");
    if (localChatId) {
      setChatid(localChatId);
    } else {
      const newChatId = Date.now().toString();
      setChatid(newChatId);
      localStorage.setItem("chatid", newChatId);
    }
  }, []);

  useEffect(() => {
    // Initialize socket connection
    socketRef.current = io("ws://127.0.0.1:8000", {
      transports: ["websocket"],
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    const socket = socketRef.current;

    // Connection event handlers
    socket.on("connect", () => {
      setIsConnected(true);
      toast.current?.show({
        severity: "success",
        summary: "Connected",
        detail: "Connected to WebSocket server",
      });
    });

    socket.on("disconnect", () => {
      setIsConnected(false);
      toast.current?.show({
        severity: "error",
        summary: "Disconnected",
        detail: "Lost connection to server",
      });
    });

    socket.on("connect_error", () => {
      toast.current?.show({
        severity: "error",
        summary: "Connection Error",
        detail: "Failed to connect to server",
      });
    });

    // Typing indicators
    socket.on("start_typing", () => {
      setIsTyping(true);
    });

    socket.on("stop_typing", () => {
      setIsTyping(false);
    });

    // Message handler
    socket.on("image", (data: { file: string }) => {
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        {
          text: "",
          displayText: "",
          isTyping: false,
          type: "ai",
          image: data.file,
        },
      ]);
    });

    socket.on("message", (data: string) => {
      setIsTyping(false);
      setMessages((prev) => {
        const lastMessage = prev[prev.length - 1];

        // If there's a last message and it's from AI, append to it
        if (lastMessage && lastMessage.type === "ai") {
          const updatedMessages = [...prev];
          updatedMessages[prev.length - 1] = {
            ...lastMessage,
            text: lastMessage.text + data,
            displayText: lastMessage.displayText + data,
          };
          return updatedMessages;
        }

        // Otherwise create a new message
        return [
          ...prev,
          {
            text: data,
            displayText: data,
            isTyping: false,
            type: "ai",
          },
        ];
      });
    }); // Connect to the server
    socket.connect();

    // Cleanup on unmount
    return () => {
      if (socket) {
        socket.removeAllListeners();
        socket.disconnect();
      }
    };
  }, []);

  return (
    <Wrapper>
      <MessageHeader
        chatid={chatid}
        setChatid={setChatid}
        setMessages={setMessages}
      />
      <MessageBox>
        <Messages messages={messages} />
        {isTyping && <Loading />}
      </MessageBox>
      <MessagePanel
        isConnected={isConnected}
        socketRef={socketRef}
        fileupload={fileupload}
        setMessages={setMessages}
        setVisible={setVisible}
        chatid={chatid}
        setFileupload={setFileupload}
      />
      <Fileuploader
        visible={visible}
        setVisible={setVisible}
        setFileupload={setFileupload}
        toast={toast}
      />
      <Toast ref={toast} />
    </Wrapper>
  );
}
