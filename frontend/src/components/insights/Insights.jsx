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

const Insights = ({ insights }) => {
  const auth = useAuth();

  return (
    <Flex mt={5} direction="column" alignItems="center" width={"80%"}>
      <Heading as="h2" size="lg">
        {insights.customer_name}
      </Heading>

      <Table mt={4} variant="simple">
        <Tbody>
          <Tr>
            <Td textAlign={"center"}>current payment</Td>
            <Td textAlign={"center"}>suggested payment</Td>
            <Td textAlign={"center"} background="teal" fontSize={25}>
              Total savings
            </Td>
          </Tr>
          <Tr>
            <Td border="none" textAlign="center">
              {Math.round(insights.pricing.prev)}$/month
            </Td>
            <Td border="none" textAlign="center">
              {Math.round(insights.pricing.suggested)}$/month
            </Td>
            <Td border="none" fontSize={25} textAlign="center">
              {Math.round(insights.pricing.prev - insights.pricing.suggested)}$
            </Td>
          </Tr>
        </Tbody>
      </Table>
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
