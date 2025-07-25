import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import MyForm from "./pages/MyForm";
import AssessmentDisplay from "./pages/AssessmentDisplay";
import AssessmentsPage from "./pages/HistoryPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <MyForm />,
  },
  {
    path: "/get_assessment",
    children: [
      {
        path: "*",
        element: <AssessmentDisplay />,
      },
    ],
  },
  {
    path: "/get_history",
    element: <AssessmentsPage />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
