# Output Event Handler Example

```Java
public static final OutputEventInterface cmdHandler = new OutputEventInterface() {
    public void outputEventHandler(Object data, String agentName, String attributeName, WMElement pWmeAdded) {
        for (int i=0; i<pWmeAdded.ConvertToIdentifier().GetNumberChildren(); i++) {
            final WMElement wChild = pWmeAdded.ConvertToIdentifier().GetChild(i);
            System.out.println("^" + wChild.GetAttribute() + " " + wChild.GetValueAsString());
        }
    }
};

agent.AddOutputHandler("do", cmdHandler, null);
agent.ExecuteCommandLine("sp {test (state <s> ^io.output-link <out>) --> (<out> ^do <d>) (<d> ^foo bar ^baz qux)}");
agent.RunSelf(2);
```

Source: <https://web.eecs.umich.edu/~soar/ijcai16/Tutorial-2016-sml.pdf>
