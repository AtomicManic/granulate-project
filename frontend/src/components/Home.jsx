import { Divider, Heading, Text } from "@chakra-ui/react";
import SliderComponent from "./util/SliderComponent";
import { React, createRef, useRef } from "react";
import UploadFile from "./UploadFile";

const Home = () => {
  const uploadFileRef = useRef(null);

  const scrollToRef = () => {
    uploadFileRef.current.scrollIntoView({ behavior: "smooth" });
  };
  return (
    <>
      <Heading m={10}>Welcome To CloudOPT</Heading>
      <Text m={10} fontSize={25}>
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
      <SliderComponent scrollToRef={scrollToRef} />
      <UploadFile ref={uploadFileRef} />
    </>
  );
};

export default Home;
