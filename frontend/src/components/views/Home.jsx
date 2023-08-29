import { Flex, Heading, Text } from "@chakra-ui/react";
import SliderComponent from "../general/SliderComponent";
import { useAuth } from "../../hooks/useAuth";

const Home = () => {
  return (
    <Flex direction="column" justifyContent="center" width="80%" m="0 auto">
      <Heading m={10} mb={3}>
        Welcome To CloudOPT
      </Heading>
      <Text m={10} mt={3} fontSize={25}>
        Leveraging state-of-the-art optimization algorithms and techniques,
        CloudOPT equips you with an extensive, detailed evaluation of your cloud
        performance. Our platform delves deep into the intricate aspects of your
        cloud operations, diagnosing areas of improvements, and flagging
        potential bottlenecks. The insights garnered from this analysis not only
        improve overall efficiency but also drive cost-effectiveness. Try it now
        for FREE!
      </Text>
      <Text m={10} fontSize={25}>
        This is how it works:
      </Text>
      <SliderComponent />
    </Flex>
  );
};

export default Home;
