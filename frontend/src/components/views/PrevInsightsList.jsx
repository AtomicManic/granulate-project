import { Button, Flex, Heading } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import CloudDivider from "../general/CloudDivider";
import axiosInstance from "../../services/axios";
import { useAuth } from "../../hooks/useAuth";
import InsightTable from "../insights/InsightTable";
import Insights from "../insights/Insights";

const PrevInsightsList = () => {
  const [insights, setInsights] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState({});
  const auth = useAuth();

  useEffect(() => {
    const getInsights = async () => {
      try {
        const response = await axiosInstance.get(
          `/requests/insights?id=${auth.user.user_id}`,
          { withCredentials: true }
        );
        setInsights(response.data);
      } catch (error) {}
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
      <Flex mt={5}>
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
      </Flex>
      {!(Object.keys(selectedFile).length === 0) ? (
        <Insights insights={selectedFile} />
      ) : (
        ""
      )}
    </Flex>
  );
};

export default PrevInsightsList;
