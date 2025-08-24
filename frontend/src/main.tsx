import { PrimeReactProvider } from "primereact/api";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";

import "primeicons/primeicons.css"; // PrimeIcons CSS
import "primereact/resources/primereact.min.css"; // Core CSS
import "primereact/resources/themes/lara-light-indigo/theme.css"; // Choose your theme

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <PrimeReactProvider>
      <App />
    </PrimeReactProvider>
  </StrictMode>
);
