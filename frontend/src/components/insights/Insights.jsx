import {
  Box,
  Button,
  Flex,
  Heading,
  Table,
  Tbody,
  Td,
  Tr,
} from "@chakra-ui/react";
import React from "react";
import InsightsList from "./InsightsList";
import { useAuth } from "../../hooks/useAuth";
import InsightTable from "./InsightTable";

const Insights = ({ insights }) => {
  const auth = useAuth();
  return (
    <Flex mt={5} direction="column" alignItems="center" width={"80%"}>
      <Heading as="h2" size="lg">
        {insights.customer_name}
      </Heading>
      <InsightTable insights={insights} />

      {auth.isAuthenticated && (
        <Button colorScheme="teal" size="lg" mb={5} mt={9}>
          Apply Suggestions
        </Button>
      )}
      <InsightsList insights={insights} />
    </Flex>
  );
};

export default Insights;
