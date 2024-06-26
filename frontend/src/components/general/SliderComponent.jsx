import {
  CarouselProvider,
  Slider,
  Slide,
  ButtonBack,
  ButtonNext,
} from "pure-react-carousel";
import "pure-react-carousel/dist/react-carousel.es.css";
import {
  Card,
  CardHeader,
  Heading,
  CardBody,
  CardFooter,
  Button,
  Text,
  Box,
  Flex,
  useBreakpointValue,
} from "@chakra-ui/react";
import { ArrowRightIcon, ArrowLeftIcon } from "@chakra-ui/icons";
import { useNavigate } from "react-router-dom";

const data = [
  {
    title: "Step #1",
    description: "Generate a cloud analysis JSON file using our custom script",
    button: true,
    buttonContent: "Learn How",
    path: "/instructions",
  },
  {
    title: "Step #2",
    description: "Upload the JSON file",
    button: true,
    buttonContent: "Go to Upload",
    path: "/upload",
    green: true,
  },
  {
    title: "Step #3",
    description: "Want to apply the suggested changes?",
    button: true,
    buttonContent: "Login",
    path: "/login",
  },
];

const CardComponent = ({ item }) => {
  const navigate = useNavigate();
  const cardWidth = useBreakpointValue({ base: "300px", sm: "md", md: "lg" });

  return (
    <Card m="10px" height="320px" fontSize="22px" w={cardWidth}>
      <CardHeader>
        <Heading size="md">{item.title}</Heading>
      </CardHeader>
      <CardBody>
        <Text textAlign="center">{item.description}</Text>
      </CardBody>
      <CardFooter justifyContent="center">
        {item?.button && (
          <Button
            onClick={() => navigate(item.path)}
            bg={item?.green ? "teal.400" : "gray.600"}
            fontSize={item?.green ? "25" : "20"}
          >
            {item.buttonContent}
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};

const SliderComponent = () => {
  const isMobile = useBreakpointValue({ base: true, lg: false });

  return (
    <Box m={10}>
      {isMobile ? (
        <CarouselProvider
          naturalSlideWidth={100}
          naturalSlideHeight={125}
          totalSlides={data.length}
          isIntrinsicHeight={true}
        >
          <Flex justifyContent="center" alignItems="center">
            <ButtonBack>
              <ArrowLeftIcon />
            </ButtonBack>
            <Box width="100%">
              <Slider>
                {data.map((item, index) => (
                  <Slide key={index} index={index}>
                    <Flex justifyContent="center">
                      <CardComponent item={item} />
                    </Flex>
                  </Slide>
                ))}
              </Slider>
            </Box>
            <ButtonNext>
              <ArrowRightIcon />
            </ButtonNext>
          </Flex>
        </CarouselProvider>
      ) : (
        <Flex justifyContent="center" alignItems="center">
          {data.map((item, index) => (
            <CardComponent key={index} item={item} />
          ))}
        </Flex>
      )}
    </Box>
  );
};

export default SliderComponent;
