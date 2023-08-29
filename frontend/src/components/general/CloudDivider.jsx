import { Box, Divider, AbsoluteCenter } from "@chakra-ui/react";
import { CloudArrowUpFill } from "react-bootstrap-icons";

const CloudDivider = () => {
  return (
    <Box position="relative" padding="10" mt="100px">
      <Divider />
      <AbsoluteCenter px="4">
        <CloudArrowUpFill fontSize={145} />
      </AbsoluteCenter>
    </Box>
  );
};

export default CloudDivider;
