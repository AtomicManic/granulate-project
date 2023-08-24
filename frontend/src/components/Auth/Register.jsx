import {
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import React from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../../services/axios";
import { useState } from "react";

const Register = () => {
  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting },
  } = useForm();

  const [errorMsgs, setErrorMsgs] = useState({});

  const navigate = useNavigate();

  const onSubmit = async (values) => {
    try {
      const response = await axiosInstance.post("/users/register", values, {
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });
      navigate("/login");
    } catch (error) {
      error.response.data?.detail === "Email already exist"
        ? setErrorMsgs({
            ...errorMsgs,
            duplicateEmail: error.response.data.detail,
          })
        : null;
    }
  };

  return (
    <Flex height="84vh" align="center" justifyContent="center">
      <Flex
        direction="column"
        alignItems="center"
        background={useColorModeValue("gray.100", "gray.700")}
        p={10}
        rounded={6}
        width="65%"
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <Heading textAlign="center" mb={7}>
            Register
          </Heading>
          <FormLabel>Personal Info</FormLabel>
          <FormControl isInvalid={errors.first_name}>
            <Input
              placeholder="First Name"
              background={useColorModeValue("gray.300", "gray.600")}
              type="text"
              size="lg"
              mt={2}
              {...register("first_name", {
                required: "This is a required field",
                minLength: {
                  value: 2,
                  message: "First name must have at least 2 characters",
                },
              })}
            />
            <FormErrorMessage>
              {errors.first_name && errors.first_name.message}
            </FormErrorMessage>
          </FormControl>
          <FormControl isInvalid={errors.last_name}>
            <Input
              placeholder="Last Name"
              background={useColorModeValue("gray.300", "gray.600")}
              type="text"
              size="lg"
              mt={6}
              mb={2}
              {...register("last_name", {
                required: "This is a required field",
                minLength: {
                  value: 2,
                  message: "Last name must have at least 2 characters",
                },
              })}
            />
            <FormErrorMessage>
              {errors.last_name && errors.last_name.message}
            </FormErrorMessage>
          </FormControl>
          <FormLabel mt={6}>Email and Password</FormLabel>
          <FormControl isInvalid={errors.email}>
            <Input
              placeholder="Email"
              autoComplete="username"
              background={useColorModeValue("gray.300", "gray.600")}
              type="email"
              size="lg"
              mt={2}
              {...register("email", { required: "This is a required field" })}
              onChange={() => setErrorMsgs({})}
            />
            <FormErrorMessage>
              {errors.email && errors.email.message}
            </FormErrorMessage>
            {errorMsgs && (
              <Text fontSize="sm" color="#fc8181">
                {errorMsgs.duplicateEmail}
              </Text>
            )}
          </FormControl>
          <FormControl isInvalid={errors.password}>
            <Input
              placeholder="Password"
              autoComplete="current-password"
              background={useColorModeValue("gray.300", "gray.600")}
              type="password"
              size="lg"
              mt={6}
              {...register("password", {
                required: "This is a required field",
                minLength: {
                  value: 8,
                  message: "password must have at least 8 characters",
                },
                maxLength: {
                  value: 24,
                  message: "password must be at most 24 characters",
                },
              })}
            />
            <FormErrorMessage>
              {errors.password && errors.password.message}
            </FormErrorMessage>
          </FormControl>
          <Button
            isLoading={isSubmitting}
            loadingText="Signing you up..."
            type="submit"
            width="100%"
            colorScheme="gray"
            variant="solid"
            mt={6}
            mb={6}
          >
            Submit
          </Button>
          <Button
            onClick={() => navigate("/login")}
            width="100%"
            colorScheme="gray"
            variant="link"
          >
            Login instead
          </Button>
        </form>
      </Flex>
    </Flex>
  );
};

export default Register;
