import React from "react";
import VmInsight from "./VmInsight";
import { Flex, Heading, Grid, Box } from "@chakra-ui/react";

const InsightsList = ({ insights }) => {
  return (
    <>
      <Heading as="h2" size="lg" mb={4}>
        Details
      </Heading>
      <Flex justifyContent="space-evenly" width={"100%"} direction="column">
        <Box>
          <Grid
            templateColumns="repeat(auto-fill, minmax(220px, 1fr))"
            gap={1}
            textAlign="center"
          >
            {insights.vms_rec.map((vm) => {
              return <VmInsight insight={vm} key={vm.id} />;
            })}
          </Grid>
        </Box>
      </Flex>
    </>
  );
};

export default InsightsList;
