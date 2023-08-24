import {
  Flex,
  Heading,
  Link,
  Text,
  Code,
  useBreakpointValue,
} from "@chakra-ui/react";
import React from "react";
import { useNavigate } from "react-router-dom";

const Instructions = () => {
  const navigate = useNavigate();
  const codeSize = useBreakpointValue({ base: "xs", sm: "sm", md: "xl" });
  const textSize = useBreakpointValue({ base: "sm", sm: "md", md: "25px" });
  const headingSize = useBreakpointValue({ base: "sm", sm: "md", md: "lg" });
  return (
    <>
      <Heading m={10} textAlign="center" bg={"gray.800"}>
        How To Create Cloud Analysis JSON
      </Heading>
      <Flex
        direction="column"
        justifyContent="center"
        width="80%"
        m="0 auto"
        p={10}
        gap={5}
        bg={"gray.700"}
        mt={8}
        pb={10}
      >
        <Heading as="h3" size={headingSize}>
          1. Download the script from{" "}
          <Link
            href="https://fm-staging.dcs-tools-experiments.infra-host.com/main"
            color={"teal.400"}
          >
            HERE
          </Link>
        </Heading>
        <Heading as="h3" size={headingSize} mt={3}>
          2. Install dependencies:
        </Heading>
        <Text fontSize={textSize} ml={8}>
          Run the script with the{" "}
          <Code fontSize={codeSize}>-install-own-deps</Code> flag to install
          required dependencies:
          <br />
          <br />
          <Code fontSize={codeSize}>
            python3 script_name.py --install-own-deps
          </Code>
        </Text>
        <Heading as="h3" size={headingSize} mt={3}>
          3. AWS Authentication
        </Heading>
        <Text fontSize={textSize} ml={8}>
          If you have AWS CLI configured, run aws sso login and enter
          "Granulate" as the company name. Alternatively, if you don't have the
          AWS CLI, you can export the environment parameters for AWS
          credentials:
          <br />
          <br />
          <Code fontSize={codeSize} width="90%">
            export AWS_ACCESS_KEY_ID=your_access_key
          </Code>
          <br />
          <br />
          <Code fontSize={codeSize} width="90%">
            export AWS_SECRET_ACCESS_KEY=your_secret_key
          </Code>
          <br />
          <br />
          <Code fontSize={codeSize} width="90%">
            export AWS_SESSION_TOKEN=your_session_token
          </Code>
        </Text>
        <Heading as="h3" size={headingSize} mt={3}>
          4. Run the script
        </Heading>
        <Text fontSize={textSize} ml={8}>
          Execute the script with appropriate parameters. Here's an example
          command:
          <br />
          <br />
          <Code fontSize={codeSize}>
            python3 script_name.py -e &lt;endpoint_url&gt; -r &lt;region&gt;
          </Code>
          <br />
          <br />
          The flags <Code fontSize={codeSize}>-e</Code> and{" "}
          <Code fontSize={codeSize}>-r</Code> are used to specify the endpoint
          URL and the AWS region respectively.
          <br /> Other optional flags are <Code fontSize={codeSize}>
            -s
          </Code>{" "}
          for SSL usage, <Code fontSize={codeSize}>-ma</Code> for multi-account
          scan and <Code fontSize={codeSize}>-sa</Code> for skipping accounts.
        </Text>
        <Heading as="h3" size={headingSize} mt={3}>
          5. Upload the output
        </Heading>
        <Text fontSize={textSize} ml={8}>
          The script generates an .xz file in the directory where you ran it.
          unzip the file using{" "}
          <Code fontSize={codeSize}>xz -d &lt;filename.xz&gt;</Code>
          and than upload it{" "}
          <Link
            onClick={() => navigate("/upload")}
            color={"teal.400"}
            fontWeight={"bold"}
          >
            HERE
          </Link>
        </Text>
        <Text mt={3} fontSize={textSize}>
          *** Please replace placeholders (like script_name.py, your_access_key,
          your_secret_key, your_session_token, &lt;endpoint_url&gt;,
          &lt;region&gt;) with actual values.
        </Text>
      </Flex>
    </>
  );
};

export default Instructions;
