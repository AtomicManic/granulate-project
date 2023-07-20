import React from "react";
import { Box, keyframes } from "@chakra-ui/react";
import { ChevronDownIcon } from "@chakra-ui/icons";
import { css } from "@emotion/react";

// Define the keyframes of the animation
const bounce = keyframes`
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-30px);
  }
  60% {
    transform: translateY(-15px);
  }
`;

// Define the animation in a CSS prop
const bounceAnimation = css`
  animation: ${bounce} 2s infinite;
`;

const BouncingArrow = ({ scrollToRef }) => {
  return (
    <Box
      onClick={scrollToRef}
      css={bounceAnimation}
      textAlign="center"
      mt={10}
      cursor="pointer"
      color={"teal.400"}
    >
      <ChevronDownIcon boxSize={20} />
    </Box>
  );
};

export default BouncingArrow;
