import { Table, Tbody, Tr, Td } from "@chakra-ui/react";

const insightTable = ({ insights }) => {
  return (
    <Table mt={4} variant="simple" fontSize={["sm", "md", "lg"]}>
      <Tbody>
        <Tr>
          <Td textAlign="center" fontSize={["xs", "sm", "md"]}>
            Current payment
          </Td>
          <Td textAlign="center" fontSize={["xs", "sm", "md"]}>
            Suggested payment
          </Td>
          <Td
            textAlign="center"
            background="teal"
            fontSize={["md", "lg", "xl"]}
          >
            Total savings
          </Td>
        </Tr>
        <Tr>
          <Td border="none" textAlign="center" fontSize={["xs", "sm", "md"]}>
            {Math.round(insights.pricing.prev)}$/month
          </Td>
          <Td border="none" textAlign="center" fontSize={["xs", "sm", "md"]}>
            {Math.round(insights.pricing.suggested)}$/month
          </Td>
          <Td border="none" fontSize={["md", "lg", "xl"]} textAlign="center">
            {Math.round(insights.pricing.prev - insights.pricing.suggested)}
            $/month
          </Td>
        </Tr>
      </Tbody>
    </Table>
  );
};

export default insightTable;
