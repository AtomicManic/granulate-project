import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import Home from "./components/views/Home";
import UploadFileView from "./components/views/UploadFileView";
import { AuthProvider, AuthConsumer } from "./contexts/JWTAuthContext";
import Navbar from "./components/general/Navbar";
import Instructions from "./components/views/Instructions";
import { useEffect } from "react";
import axiosInstance from "./services/axios";
import PublicRoute from "./components/Auth/PublicRoute";
import PrevInsightsList from "./components/views/PrevInsightsList";
import AuthRoute from "./components/Auth/AuthRoute";
import LogoutLoader from "./components/general/LogoutLoader";

function App() {
  useEffect(() => {
    const getCookie = async () => {
      const res = await axiosInstance.get("/auth/cookie", {
        withCredentials: true,
      });
    };
    getCookie();
  }, []);

  return (
    <>
      <AuthProvider>
        <Router>
          <AuthConsumer>
            {(auth) => (
              <>
                <Navbar />
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/Instructions" element={<Instructions />} />
                  <Route path="/upload" element={<UploadFileView />} />
                  <Route
                    path="/login"
                    element={
                      <PublicRoute restricted={true}>
                        <Login />
                      </PublicRoute>
                    }
                  />
                  <Route
                    path="/register"
                    element={
                      <PublicRoute restricted={true}>
                        <Register />
                      </PublicRoute>
                    }
                  />
                  <Route
                    path="/my-insights"
                    element={
                      <AuthRoute restricted={true}>
                        <PrevInsightsList />
                      </AuthRoute>
                    }
                  />
                  <Route path="/logout" element={<LogoutLoader />} />
                  <Route path="/*all" element={<Navigate to="/" replace />} />
                </Routes>
              </>
            )}
          </AuthConsumer>
        </Router>
      </AuthProvider>
    </>
  );
}

export default App;
