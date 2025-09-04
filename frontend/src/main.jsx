import React from "react"
import { createRoot } from "react-dom/client"
import './index.css'
import { AppRouter } from "./AppRouter"

const root = createRoot(document.getElementById("root"))
root.render(<AppRouter />)
