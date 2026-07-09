import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './layouts/MainLayout';
import DashboardPage from './pages/DashboardPage';
import LogInteractionPage from './pages/LogInteractionPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected Routes wrapped in MainLayout */}
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          } 
        >
          <Route index element={<DashboardPage />} />
          <Route path="log-interaction" element={<LogInteractionPage />} />
          {/* Other routes will go here: history, hcps, analytics, settings */}
        </Route>
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
