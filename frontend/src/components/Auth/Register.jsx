import {
  Button,
  Divider,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  useColorMode,
  useColorModeValue,
} from "@chakra-ui/react";
import React from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

const Register = () => {
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
    <Flex height="100vh" align="center" justifyContent="center">
      <Flex
        direction="column"
        alignItems="center"
        background={useColorModeValue("gray.100", "gray.700")}
        p={12}
        rounded={6}
      >
        <form onSubmit={handleSubmit(onSubmit)}>
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
                  value: 5,
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
              background={useColorModeValue("gray.300", "gray.600")}
              type="email"
              size="lg"
              mt={2}
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
