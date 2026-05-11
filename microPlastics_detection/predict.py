results = model.predict(
    source='downloads/dataset_final/',
    save=True,
    save_txt=True,
    conf=0.5,
    show_labels=False,
    show_conf=False
)