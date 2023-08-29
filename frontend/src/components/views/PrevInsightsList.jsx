import { Button, Flex, Grid, Heading, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import CloudDivider from "../general/CloudDivider";
import axiosInstance from "../../services/axios";
import { useAuth } from "../../hooks/useAuth";
import Insights from "../insights/Insights";

const PrevInsightsList = () => {
  const [insights, setInsights] = useState([]);
  const [message, setMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState({});
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const getInsights = async () => {
      try {
        const response = await axiosInstance.get(
          `/requests/insights?id=${auth.user.user_id}`,
          { withCredentials: true }
        );
        if (response.data.length == 0) {
          setMessage("Nothing to show yet...");
        } else if (!response) {
          setMessage("Nothing to show yet...");
        }
        setInsights(response.data);
      } catch (error) {
        setMessage("Nothing to show yet...");
      }
    };
    getInsights();
  }, []);

  const handleInsightDisplay = (id) => {
    const filteredArray = insights.filter((item) => item.insights.id === id);
    setSelectedFile(filteredArray[0].insights);
  };
  return (
    <Flex justifyContent="center" direction="column" alignItems="center">
      <CloudDivider />
      <Heading mt={5}>My Insights</Heading>
      {!message && (
        <Grid
          templateColumns="repeat(auto-fill, minmax(170px, 1fr))"
          gap={1}
          textAlign="center"
          mt={5}
          width="80%"
        >
          {insights.map((insight) => {
            const dateStr = insight.created_at.split("T")[0];
            return (
              <Button
                key={insight.insights.id}
                onClick={() => handleInsightDisplay(insight.insights.id)}
                m={2}
              >
                {dateStr}
              </Button>
            );
          })}
        </Grid>
      )}
      {!message && !(Object.keys(selectedFile).length === 0) ? (
        <Insights insights={selectedFile} />
      ) : (
        ""
      )}
      {message && (
        <>
          <Text mt={5} fontSize="25px">
            {message}
          </Text>
          <Button onClick={() => navigate("/upload")} mt={5} colorScheme="teal">
            Upload File
          </Button>
        </>
      )}
    </Flex>
  );
};

export default PrevInsightsList;
