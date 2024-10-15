---
counter: True
comment: True
---

# Weights & Biases

!!! abstract
    wandb 常用命令

## wandb.init

> [!info] wandb.init
> 初始化一个新的运行，返回一个 `wandb.Run` 对象。
>
> ```py
> run = wandb.init(
>     project="project_name",
>     entity="entity_name",
>     name="run_name",
>     config=config, # 超参数
>     ...
> )
> 
> ...
>
> run.finish()
> ```

## wandb.log

> [!info] wandb.log
> 使用 log 记录运行中的数据，例如标量、图像、视频、直方图、绘图和表格。
>
> ```py
> wandb.log(
>     data: Dict[str, Any],
>     step: Optional[int] = None,
>     commit: Optional[bool] = None,
>     sync: Optional[bool] = None
> ) -> None
> ```
>
> ```python
> run.log({
>     "train/accuracy": 0.9,
>     "train/loss": 30,
>     "validate/accuracy": 0.8,
>     "validate/loss": 20,
> })
> ```

## wandb.Image

> [!info] wandb.Image
> 格式化图像以记录到W&B。
> 
> ```python
> Image(
>     data_or_path: "ImageDataOrPathType",
>     mode: Optional[str] = None,
>     caption: Optional[str] = None,
>     grouping: Optional[int] = None,
>     classes: Optional[Union['Classes', Sequence[dict]]] = None,
>     boxes: Optional[Union[Dict[str, 'BoundingBoxes2D'], Dict[str, dict]]] = None,
>     masks: Optional[Union[Dict[str, 'ImageMask'], Dict[str, dict]]] = None,
>     file_type: Optional[str] = None
> ) -> None
> ```
>
> ```python
> examples = []
> for i in range(3):
>     pixels = np.random.randint(low=0, high=256, size=(100, 100, 3))
>     image = wandb.Image(pixels, caption=f"random field {i}")
>     examples.append(image)
> run.log({"examples": examples})
> ```

## wandb.Table

> [!info] wandb.Table
> Table 类，用于显示和分析表格数据。
>
> ```python
> Table(
>     columns=None,
>     data=None,
>     rows=None,
>     dataframe=None,
>     dtype=None,
>     optional=(True),
>     allow_mixed_types=(False)
> )
> ```
>
> ```python
> my_table = wandb.Table(columns=["a", "b"], data=[["a1", "b1"], ["a2", "b2"]])
> run.log({"Table Name": my_table})
> ```

## Artifact

> [!info] Artifact
> 用于数据集和模型版本控制的构件。
>
> ```python
> Artifact(
>     name: str,
>     type: str,
>     description: Optional[str] = None,
>     metadata: Optional[Dict[str, Any]] = None,
>     incremental: bool = (False),
>     use_as: Optional[str] = None
> ) -> None
> ```


## Data Types

| Data Types        | Description                                                     |
| ----------------- | --------------------------------------------------------------- |
| `Audio`           | Wandb class for audio clips.                                    |
| `BoundingBoxes2D` | Format images with 2D bounding box overlays for logging to W&B. |
| `Graph`           | Wandb class for graphs.                                         |
| `Histogram`       | wandb class for histograms.                                     |
| `Html`            | Wandb class for arbitrary html.                                 |
| `Image`           | Format images for logging to W&B.                               |
| `ImageMask`       | Format image masks or overlays for logging to W&B.              |
| `Molecule`        | Wandb class for 3D Molecular data.                              |
| `Object3D`        | Wandb class for 3D point clouds.                                |
| `Plotly`          | Wandb class for plotly plots.                                   |
| `Table`           | The Table class used to display and analyze tabular data.       |
| `Video`           | Format a video for logging to W&B.                              |
| `WBTraceTree`     | Media object for trace tree data.                               |



## Reference

- [wandb 官方文档](https://docs.wandb.ai)
- [wandb 快速入门使用教程](https://blog.csdn.net/weixin_42855362/article/details/125107297)
- [使用 wandb 可视化训练过程](https://datawhalechina.github.io/thorough-pytorch/%E7%AC%AC%E4%B8%83%E7%AB%A0/7.4%20%E4%BD%BF%E7%94%A8wandb%E5%8F%AF%E8%A7%86%E5%8C%96%E8%AE%AD%E7%BB%83%E8%BF%87%E7%A8%8B.html)