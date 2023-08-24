import React, { useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { useNavigate, useLocation, Navigate } from "react-router-dom";

const PublicRoute = ({ children, restricted }) => {
  const navigate = useNavigate();
  const auth = useAuth();

  useEffect(() => {
    if (auth.isAuthenticated && restricted) {
      navigate("/");
    }
  }, [auth.isAuthenticated, restricted, navigate]);

  return auth.isAuthenticated && restricted ? null : children;
};

export default PublicRoute;
