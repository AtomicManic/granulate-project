import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import Home from "./components/views/Home";
import { AuthProvider } from "./contexts/JWTAuthContext";
import Navbar from "./components/Navbar";
import Instructions from "./components/views/Instructions";

function App() {
  return (
    <>
      <AuthProvider>
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/Instructions" element={<Instructions />} />
          </Routes>
        </Router>
      </AuthProvider>
    </>
  );
}

export default App;
