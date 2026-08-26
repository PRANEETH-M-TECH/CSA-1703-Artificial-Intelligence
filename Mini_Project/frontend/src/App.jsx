import { Routes, Route, Navigate } from "react-router-dom";
import NavShell from "./components/NavShell";
import ProtectedRoute from "./components/ProtectedRoute";

import Splash from "./pages/Splash";
import Onboarding from "./pages/Onboarding";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import HomeDashboard from "./pages/HomeDashboard";
import TaskList from "./pages/TaskList";
import AddEditTask from "./pages/AddEditTask";
import ScheduleView from "./pages/ScheduleView";
import ConflictAlerts from "./pages/ConflictAlerts";
import ConflictResolution from "./pages/ConflictResolution";
import Insights from "./pages/Insights";
import Recommendations from "./pages/Recommendations";
import Profile from "./pages/Profile";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Splash />} />
      <Route path="/onboarding" element={<Onboarding />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      <Route
        path="/app"
        element={
          <ProtectedRoute>
            <NavShell />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="home" replace />} />
        <Route path="home" element={<HomeDashboard />} />

        <Route path="tasks" element={<TaskList />} />
        <Route path="tasks/new" element={<AddEditTask />} />
        <Route path="tasks/:id/edit" element={<AddEditTask />} />

        <Route path="schedule" element={<ScheduleView />} />
        <Route path="schedule/conflicts" element={<ConflictAlerts />} />
        <Route path="schedule/conflicts/:id" element={<ConflictResolution />} />

        <Route path="insights" element={<Insights />} />
        <Route path="insights/recommendations" element={<Recommendations />} />

        <Route path="profile" element={<Profile />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
