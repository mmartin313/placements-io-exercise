import { createBrowserRouter } from "react-router-dom";

import { Campaigns } from "./views/Campaigns";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Campaigns />,
  },
]);
