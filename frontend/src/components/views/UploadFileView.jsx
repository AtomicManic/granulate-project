import React from "react";
import UploadFile from "../insights/UploadFile";
import CloudDivider from "../general/CloudDivider";
import { useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  Heading,
  Flex,
  useBreakpointValue,
  Text,
  Button,
} from "@chakra-ui/react";
import axiosInstance from "../../services/axios";
import { useAuth } from "../../hooks/useAuth";
import VmInsight from "../insights/VmInsight";
import Insights from "../insights/Insights";
import { Navigate, useNavigate } from "react-router-dom";

const UploadFileView = () => {
  const [fileName, setFileName] = useState("");
  const isMobile = useBreakpointValue({ base: true, md: false });
  const [validJsonMessage, setValidJsonMessage] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [insights, setInsights] = useState({});
  const navigate = useNavigate();
  const auth = useAuth();

  const handleFileSubmit = async (content) => {
    let response;
    let id;
    setIsLoading(true);
    const { user } = JSON.parse(localStorage.getItem("authState"));
    if (auth.isAuthenticated) {
      if (auth.user) {
        id = auth.user.user_id;
      } else if (user !== null) {
        id = user.user_id;
      }
    } else {
      id = "";
    }
    try {
      response = await axiosInstance.post(
        `/requests?id=${id}`,
        { data: content },
        {
          withCredentials: true,
        }
      );
      setInsights(response.data);
    } catch (error) {
      setMessage(
        error?.response.data?.detail
          ? error?.response.data?.detail
          : "Something went wrong... Please try again in a few minutes"
      );
    }
    setIsLoading(false);
  };

  const onDrop = React.useCallback((acceptedFiles) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const content = JSON.parse(reader.result);
        setFileName(acceptedFiles[0].path);
        handleFileSubmit(content);
      } catch (e) {
        setValidJsonMessage("File contents are not valid JSON");
      }
    };

    try {
      reader.readAsText(acceptedFiles[0]);
    } catch (error) {
      setMessage("File contents are not valid JSON");
    }
  });

  const handleTryAgain = () => {
    setFileName("");
    setMessage("");
    navigate("/upload");
  };

  return (
    <>
      <CloudDivider />
      <Flex direction="column" justifyContent={"center"} alignItems="center">
        <Heading mt={6} as="h1" size="2xl">
          {fileName ? "Insights" : "Upload JSON File"}
        </Heading>

        {!message ? (
          <UploadFile
            fileName={fileName}
            onDrop={onDrop}
            isMobile={isMobile}
            message={validJsonMessage}
            isLoading={isLoading}
          />
        ) : (
          <>
            <Text mt={5} fontSize="25px">
              {message}
            </Text>
            <Button onClick={() => handleTryAgain()}>Try again</Button>
          </>
        )}
        {!(Object.keys(insights).length === 0) && (
          <Insights insights={insights} />
        )}
      </Flex>
    </>
  );
};

export default UploadFileView;
