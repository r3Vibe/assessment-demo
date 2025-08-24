export interface Message {
  text: string;
  displayText: string;
  isTyping: boolean;
  type: "human" | "ai";
  image?: string;
}
