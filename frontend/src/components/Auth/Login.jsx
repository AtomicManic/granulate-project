import {
  Button,
  Divider,
  Flex,
  FormControl,
  FormErrorMessage,
  Heading,
  Input,
  useColorMode,
  useColorModeValue,
  Text,
  // FormHeading,
} from "@chakra-ui/react";
import React from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting },
  } = useForm();

  const navigate = useNavigate();

  const onSubmit = (values) => {
    console.log(values);
  };

  return (
    <Flex height="70vh" align="center" justifyContent="center">
      <Flex
        direction="column"
        alignItems="center"
        background={useColorModeValue("gray.100", "gray.700")}
        p={10}
        rounded={6}
        width="80%"
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <Heading mb={7}>Login</Heading>
          <FormControl isInvalid={errors.email}>
            <Input
              placeholder="Email"
              background={useColorModeValue("gray.300", "gray.600")}
              type="email"
              size="lg"
              {...register("email", { required: "This is a required field" })}
            />
            <FormErrorMessage>
              {errors.email && errors.email.message}
            </FormErrorMessage>
          </FormControl>
          <FormControl isInvalid={errors.password}>
            <Input
              placeholder="Password"
              background={useColorModeValue("gray.300", "gray.600")}
              type="password"
              size="lg"
              mt={6}
              {...register("password", {
                required: "This is a required field",
              })}
            />
            <FormErrorMessage>
              {errors.password && errors.password.message}
            </FormErrorMessage>
          </FormControl>
          <Button
            isLoading={isSubmitting}
            loadingText="Logging in..."
            type="submit"
            width="100%"
            colorScheme="gray"
            variant="solid"
            mt={6}
            mb={6}
          >
            Login
          </Button>
          <Flex direction="row">
            <Text>Not Registered yet?</Text>
            <Button
              onClick={() => navigate("/register", { replace: true })}
              colorScheme="gray"
              variant="link"
              mb={6}
              ml={2}
              justifyContent="flex-start"
              fontWeight="700"
            >
              Sign up
            </Button>
          </Flex>
          <Button
            onClick={() => navigate("/", { replace: true })}
            width="100%"
            colorScheme="gray"
            variant="link"
            mt={6}
          >
            Continue as guest
          </Button>
        </form>
      </Flex>
    </Flex>
  );
};

export default Login;
