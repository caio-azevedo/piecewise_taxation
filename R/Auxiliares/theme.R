extrafont::loadfonts()
tema <- ggthemes::theme_hc() +
  theme(axis.title = element_text(
    family = "Times New Roman",
    face = "bold",
    size = 20
  ),
  axis.text = element_text(
    family = "Times New Roman",
    size = 15
  ),
  plot.caption = element_text(
    family = "Times New Roman",
    face = "bold",
    size = 15,
    hjust = 1
  ),
  legend.text = element_text(
    family = "Times New Roman",
    face = "bold",
    size = 14
  ),
  legend.title = element_text(
    family = "Times New Roman",
    size = 14 
    ),
  strip.text = element_text(
    family = "Times New Roman",
    size=14
  ))
