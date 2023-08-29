import { useEffect } from "react";
import { Flex, Spinner, Text } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const LogoutLoader = () => {
  const navigate = useNavigate();
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/");
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigate]);
  return (
    <Flex justifyContent="center" alignItems="center" direction="column">
      <Spinner size="xl" mt="100px" color="teal.400"></Spinner>
      <Text mt={5} color="teal.400">
        logging You out...
      </Text>
    </Flex>
  );
};

export default LogoutLoader;
