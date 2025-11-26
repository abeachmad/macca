import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { MaccaProvider } from "@/context/MaccaContext";
import { Toaster } from "@/components/ui/toaster";

// Pages
import Welcome from "@/pages/Welcome";
import Dashboard from "@/pages/Dashboard";
import LiveConversation from "@/pages/LiveConversation";
import GuidedLesson from "@/pages/GuidedLesson";
import PronunciationCoach from "@/pages/PronunciationCoach";
import Profile from "@/pages/Profile";

function App() {
  return (
    <MaccaProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/live-conversation" element={<LiveConversation />} />
          <Route path="/guided-lesson" element={<GuidedLesson />} />
          <Route path="/pronunciation-coach" element={<PronunciationCoach />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </MaccaProvider>
  );
}

export default App;
