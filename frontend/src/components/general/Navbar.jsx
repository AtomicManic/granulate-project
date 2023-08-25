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
import { CloudArrowUp, BoxArrowRight } from "react-bootstrap-icons";
import { useAuth } from "../../hooks/useAuth";

const Navbar = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();
  const navigate = useNavigate();
  const auth = useAuth();

  const handleLogout = () => {
    auth.logout();
    navigate("/");
  };

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
        <CloudArrowUp fontSize="30" />
        <Text
          fontSize="xl"
          fontWeight="bold"
          mr={8}
          ml={3}
          onClick={() => navigate("/")}
          cursor="pointer"
        >
          CloudOPT
        </Text>
        {!isMobileNav && (
          <>
            <Button
              onClick={() => navigate("/upload")}
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
            {auth.isAuthenticated && (
              <Button
                onClick={() => navigate("/my-insights")}
                colorScheme="teal"
                variant="link"
                mr={3}
                _hover={{ color: "white" }}
              >
                My Insights
              </Button>
            )}
          </>
        )}
      </Flex>
      {!auth.isAuthenticated ? (
        <Box display={isMobileNav ? "none" : "block"}>
          <Button
            onClick={() => navigate("/login")}
            colorScheme="teal"
            variant="link"
            _hover={{ color: "white" }}
          >
            Login
          </Button>
          <Button
            onClick={() => navigate("/register")}
            ml={5}
            colorScheme="teal"
            variant="solid"
            color={"gray.600"}
          >
            Signup
          </Button>
        </Box>
      ) : !isMobileNav ? (
        <Flex
          flexDirection="row"
          justifyContent="center"
          alignItems="center"
          gap={5}
        >
          <Text fontWeight={700}>Hello {auth?.user?.first_name}</Text>

          <Button
            onClick={() => handleLogout()}
            colorScheme="teal"
            variant="link"
            _hover={{ color: "white" }}
            display="flex"
            gap={2}
          >
            logout
          </Button>
        </Flex>
      ) : (
        ""
      )}
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
                  onClick={() => navigate("/upload")}
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
              {!auth.isAuthenticated && (
                <>
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
                </>
              )}
            </DrawerFooter>
          </DrawerContent>
        </DrawerOverlay>
      </Drawer>
    </Flex>
  );
};

export default Navbar;
