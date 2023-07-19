import React from "react";
import {
  Box,
  Flex,
  Text,
  Button,
  IconButton,
  useBreakpointValue,
  useDisclosure,
} from "@chakra-ui/react";
import { HamburgerIcon } from "@chakra-ui/icons";
import {
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();
  const navigate = useNavigate();

  const isMobileNav = useBreakpointValue({ base: true, md: false });

  return (
    <Flex
      alignItems="center"
      justifyContent="space-between"
      py={4}
      px={8}
      bg="teal.400"
      color="white"
    >
      <Flex>
        <Text fontSize="xl" fontWeight="bold" mr={8}>
          CloudOPT
        </Text>
        {!isMobileNav && (
          <>
            <Button
              onClick={() => navigate("/")}
              colorScheme="teal"
              variant="link"
              mr={3}
              _hover={{ color: "white" }}
            >
              Upload File
            </Button>
            <Button
              onClick={() => navigate("/instructions")}
              colorScheme="teal"
              variant="link"
              mr={3}
              _hover={{ color: "white" }}
            >
              Creat JSON File
            </Button>
          </>
        )}
      </Flex>
      <Box display={isMobileNav ? "none" : "block"}>
        <Button
          onClick={() => navigate("/login")}
          colorScheme="teal"
          variant="link"
        >
          Login
        </Button>
        <Button
          onClick={() => navigate("/register")}
          ml={5}
          colorScheme="teal"
          variant="solid"
        >
          Signup
        </Button>
      </Box>
      <IconButton
        ref={btnRef}
        colorScheme="teal"
        aria-label="Open Menu"
        variant="outline"
        icon={<HamburgerIcon />}
        display={isMobileNav ? "block" : "none"}
        onClick={onOpen}
      />

      <Drawer
        isOpen={isOpen}
        placement="right"
        onClose={onClose}
        finalFocusRef={btnRef}
      >
        <DrawerOverlay>
          <DrawerContent>
            <DrawerCloseButton />
            <DrawerHeader>Menu</DrawerHeader>

            <DrawerBody mt={6}>
              <Flex direction="column" alignItems="flex-start">
                <Button
                  onClick={() => navigate("/")}
                  colorScheme="teal"
                  variant="link"
                  mb={5}
                  fontSize={23}
                  _hover={{ color: "white" }}
                >
                  Upload File
                </Button>
                <Button
                  onClick={() => navigate("/instructions")}
                  colorScheme="teal"
                  variant="link"
                  fontSize={23}
                  _hover={{ color: "white" }}
                >
                  Creat JSON File
                </Button>
              </Flex>
            </DrawerBody>

            <DrawerFooter borderTopWidth="1px">
              <Button
                onClick={() => navigate("/login")}
                colorScheme="teal"
                variant="link"
              >
                Login
              </Button>
              <Button
                onClick={() => navigate("/register")}
                ml={5}
                colorScheme="teal"
                variant="solid"
              >
                Signup
              </Button>
            </DrawerFooter>
          </DrawerContent>
        </DrawerOverlay>
      </Drawer>
    </Flex>
  );
};

export default Navbar;
