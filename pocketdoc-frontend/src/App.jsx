import { Routes, Route, Navigate } from 'react-router-dom';
import Chat from './pages/Chat';
import History from './pages/History';
import Profile from './pages/Profile';
import Analytics from './pages/Analytics';
import DashboardLayout from './layouts/DashboardLayout';

function App() {
  return (
    <DashboardLayout>
      <Routes>
        <Route path="/" element={<Navigate to="/chat" replace />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/history" element={<History />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </DashboardLayout>
  );
}
export default App;
