import { useEffect } from "react";
import { useAuth } from "../../hooks/useAuth";
import { useNavigate } from "react-router-dom";

const PublicRoute = ({ children, restricted }) => {
  const navigate = useNavigate();
  const auth = useAuth();

  useEffect(() => {
    if (!auth.isAuthenticated && restricted) {
      navigate("/");
    }
  }, [auth.isAuthenticated, restricted, navigate]);

  return auth.isAuthenticated && restricted ? children : null;
};

export default PublicRoute;
