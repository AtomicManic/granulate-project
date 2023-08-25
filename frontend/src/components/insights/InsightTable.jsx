import React from "react";
import { Table, Tbody, Tr, Td } from "@chakra-ui/react";

const insightTable = ({ insights }) => {
  return (
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
  );
};

export default insightTable;
