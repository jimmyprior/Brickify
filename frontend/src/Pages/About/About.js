import "./About.css"


function EmailContainer(props) {
    const chars = props.email.split("");
    
    let charMap = chars.map((letter, index) => {
        return <p className="special-text-char" key={index}>{letter}</p>
    })

    for (let letter of "nope") {
        charMap.splice(
            Math.floor(Math.random() * charMap.length), 
            0, 
            <p className="special-text-char" style={{
                display: "none"
            }} key={charMap.length + 1}>{letter}</p>
        );
    }

    return <div className="special-text-cont">
        {charMap}
    </div> 
}

function About() {
    return <div id="about-container">
        <h2>Hey, I’m Jimmy </h2> 
        <p>
            I spent my childhood captivated by LEGO but building in the physical world proved challenging— 
            I had big ideas but lacked the means to execute them. 
            Coding offered me something that the physical world couldn’t— 
            freedom from material constraints.
            Brickify is a bridge between these two worlds connecting building in the digital world with physical outputs. 
        </p>
        <p>
            I coded the original version of Brickify (BrickPY) in 2019 as a sophomore in high school. 
            It had no UI and was simply a Python program that could convert images to brick mosaics and export them to different LEGO® marketplaces. 
        </p>
        <p>
            Examples of some of the old renderings: 
        </p>
        <img className="about-example-img" src="https://i.imgur.com/J6310Cq.png"></img>
        <img className="about-example-img" src="https://i.imgur.com/BBMXfdM.jpg"></img>
        <p>
            I rewrote the code my senior year of high school and made significant improvements to the mosaic making algorithm as well as building a website interface which is now this site. 
            There are still a lot of changes I would like to make—mainly rewriting parts of the mosaic making program in Rust or C++ and creating a UI for a lot of features that exist solely in the backend—
            but at the moment I plan on taking a break from working on this project.
        </p>
        <p>
            I’m currently studying electrical engineering at the University of Rhode Island (URI). For questions about REST API access or any other inquires feel free to send me an email. For DMCA related inquires see the help page. 
        </p>
        <EmailContainer email="jimmy@brickify.art"></EmailContainer>
    </div>
}

export default About;