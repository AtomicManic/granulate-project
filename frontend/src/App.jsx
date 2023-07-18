import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import Home from "./components/Home";
import { AuthProvider } from "./contexts/JWTAuthContext";

function App() {
  return (
    <>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </Router>
      </AuthProvider>
    </>
  );
}

export default App;
