import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import 'bootstrap-icons/font/bootstrap-icons.css';
import '../styles/index.css'
import App from './App.tsx'

let root_elm = document.getElementById('root')!;
root_elm.setAttribute("data-bs-theme", "light");
let root = createRoot(root_elm);
root.render(
  <StrictMode>
    <App />
  </StrictMode>,
);