# Load libraries
library(shiny)
library(ggplot2)
library(dplyr)

# Import dataset
adult <- read.csv("adult.csv", strip.white = TRUE)
# Convert column names to lowercase for consistency
names(adult) <- tolower(names(adult))

# Filter dataset to only contain the 5 specified countries
adult <- adult %>% 
  filter(native_country %in% c("United-States", "Canada", "Mexico", "Germany", "Philippines"))

# Define UI
ui <- fluidPage(
  # Task 1: Add application title in the UI
  titlePanel("Trends in Demographics and Income"),
  
  # Task 2: Add first fluidRow to select input for country in UI
  fluidRow(
    column(12, 
      wellPanel(
        selectInput(
          inputId = "country", 
          label = "Select Country", 
          choices = c("United-States", "Canada", "Mexico", "Germany", "Philippines"),
          selected = "United-States"
        )
      )
    )
  ),
  
  # Task 3: Add second fluidRow to control how to plot the continuous variables in UI
  fluidRow(
    column(3,
      wellPanel(
        p("Select a continuous variable and graph type to view on the right."),
        radioButtons(
          inputId = "continuous_variable",
          label = "Continuous",
          choices = c("age", "hours_per_week")
        ),
        radioButtons(
          inputId = "graph_type",
          label = "Graph",
          choices = c("histogram", "boxplot")
        )
      )
    ),
    column(9,
      plotOutput("p1")
    )
  ),
  
  # Task 4: Add third fluidRow to control how to plot the categorical variables in UI
  fluidRow(
    column(3,
      wellPanel(
        p("Select a categorical variable and toggle stacking to view on the right."),
        radioButtons(
          inputId = "categorical_variable",
          label = "Categorical",
          choices = c("education", "workclass", "sex")
        ),
        checkboxInput(
          inputId = "is_stacked",
          label = "Stack Bars",
          value = FALSE
        )
      )
    ),
    column(9,
      plotOutput("p2")
    )
  )
)

# Define server logic
server <- function(input, output) {
  
  # Filter data based on selected country
  df_country <- reactive({
    adult %>% filter(native_country == input$country)
  })
  
  # Task 5: Create logic to plot histogram or boxplot in server
  output$p1 <- renderPlot({
    if (input$graph_type == "histogram") {
      # Task 5.2: Show the histogram of the "hours_per_week"
      ggplot(df_country(), aes_string(x = input$continuous_variable)) +
        geom_histogram(bins = 30, fill = "dodgerblue", color = "white") +
        facet_wrap(~prediction) +
        labs(title = paste("Histogram of", input$continuous_variable, "by Income Level"),
             x = input$continuous_variable,
             y = "Count") +
        theme_minimal() +
        theme(legend.position = "bottom", axis.text.x = element_text(angle = 45, hjust = 1))
    } else {
      # Task 5.1: Show the boxplot of the "age" variable
      ggplot(df_country(), aes_string(y = input$continuous_variable)) +
        geom_boxplot(fill = "dodgerblue", color = "black") +
        coord_flip() +
        facet_wrap(~prediction) +
        labs(title = paste("Boxplot of", input$continuous_variable, "by Income Level"),
             y = input$continuous_variable) +
        theme_minimal() +
        theme(legend.position = "bottom", axis.text.x = element_text(angle = 45, hjust = 1))
    }
  })
  
  # Task 6: Create logic to plot faceted bar chart or stacked bar chart in server
  output$p2 <- renderPlot({
    p <- ggplot(df_country(), aes_string(x = input$categorical_variable)) +
      labs(y = "Number of People", title = paste("Trend of", input$categorical_variable)) +
      theme_minimal() +
      theme(legend.position = "bottom", axis.text.x = element_text(angle = 45, hjust = 1))
    
    if (input$is_stacked) {
      # Task 6.2: Show the stacked bar chart for the "education" variable
      p + geom_bar(aes(fill = prediction))
    } else {
      # Task 6.1: Show the faceted unstacked bar chart for the "workclass" variable
      p + geom_bar(aes_string(fill = input$categorical_variable)) +
        facet_wrap(~prediction)
    }
  })
}

# Run the application 
shinyApp(ui = ui, server = server)
